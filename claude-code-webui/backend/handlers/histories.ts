import { Context } from "hono";
import type { HistoryListResponse } from "../../shared/types.ts";
import { validateEncodedProjectName } from "../history/pathUtils.ts";
import { parseAllHistoryFiles } from "../history/parser.ts";
import { groupConversations } from "../history/grouping.ts";
import { logger } from "../utils/logger.ts";
import { stat } from "../utils/fs.ts";
import { getHomeDir } from "../utils/os.ts";

/**
 * Handles GET /api/projects/:encodedProjectName/histories requests
 * Fetches conversation history list for a specific project
 * @param c - Hono context object with config variables
 * @returns JSON response with conversation history list
 */
export async function handleHistoriesRequest(c: Context) {
  try {
    const encodedProjectName = c.req.param("encodedProjectName");

    if (!encodedProjectName) {
      return c.json({ error: "Encoded project name is required" }, 400);
    }

    if (!validateEncodedProjectName(encodedProjectName)) {
      return c.json({ error: "Invalid encoded project name" }, 400);
    }

    logger.history.debug(
      `Fetching histories for encoded project: ${encodedProjectName}`,
    );

    // Get home directory
    const homeDir = getHomeDir();
    if (!homeDir) {
      return c.json({ error: "Home directory not found" }, 500);
    }

    // Build history directory path directly from encoded name
    const historyDir = `${homeDir}/.claude/projects/${encodedProjectName}`;

    logger.history.debug(`History directory: ${historyDir}`);

    // Check if the directory exists
    try {
      const dirInfo = await stat(historyDir);
      if (!dirInfo.isDirectory) {
        return c.json({ error: "Project not found" }, 404);
      }
    } catch (error) {
      // Handle file not found errors in a cross-platform way
      if (error instanceof Error && error.message.includes("No such file")) {
        return c.json({ error: "Project not found" }, 404);
      }
      throw error;
    }

    const conversationFiles = await parseAllHistoryFiles(historyDir);

    logger.history.debug(
      `Found ${conversationFiles.length} conversation files`,
    );

    // Filter out conversations where the only user message is "Warmup"
    const filteredConversationFiles = conversationFiles.filter((conv) => {
      const userMessages = conv.messages.filter((msg) => msg.type === "user");

      // If there's exactly one user message and it's "Warmup", filter it out
      if (userMessages.length === 1) {
        const userMessage = userMessages[0];
        const messageContent = userMessage.message?.content;

        // Handle both string and array content formats
        let textContent = "";
        if (typeof messageContent === "string") {
          textContent = messageContent;
        } else if (Array.isArray(messageContent)) {
          // Extract text from array format
          for (const item of messageContent) {
            if (typeof item === "object" && item && "text" in item) {
              textContent = String(item.text);
              break;
            }
          }
        }

        // Filter out if the only user message is "Warmup" (case-insensitive)
        if (textContent.trim().toLowerCase() === "warmup") {
          return false;
        }
      }

      return true;
    });

    logger.history.debug(
      `After filtering warmup-only conversations: ${filteredConversationFiles.length} conversation files`,
    );

    // Group conversations and remove duplicates
    const conversations = groupConversations(filteredConversationFiles);

    logger.history.debug(
      `After grouping: ${conversations.length} unique conversations`,
    );

    const response: HistoryListResponse = {
      conversations,
    };

    return c.json(response);
  } catch (error) {
    logger.history.error("Error fetching conversation histories: {error}", {
      error,
    });

    return c.json(
      {
        error: "Failed to fetch conversation histories",
        details: error instanceof Error ? error.message : String(error),
      },
      500,
    );
  }
}
