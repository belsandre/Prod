const syntaxHighlight = require("@11ty/eleventy-plugin-syntaxhighlight");
const eleventyNavigation = require("@11ty/eleventy-navigation");
const markdownIt = require("markdown-it");
const markdownItAnchor = require("markdown-it-anchor");
const path = require("path");
const fs = require("fs");
const { parse } = require("csv-parse/sync");

module.exports = function(eleventyConfig, username) {
  // Prevent JSON files from being parsed as data files
  // Only use .11tydata.json for data files
  eleventyConfig.setDataFileSuffixes(['.11tydata.json', '.11tydata.js']);

  // Plugins
  eleventyConfig.addPlugin(syntaxHighlight);
  eleventyConfig.addPlugin(eleventyNavigation);

  // Markdown configuration
  const markdownOptions = {
    html: true,
    breaks: true,
    linkify: true
  };

  const markdownLib = markdownIt(markdownOptions).use(markdownItAnchor, {
    permalink: markdownItAnchor.permalink.headerLink()
  });

  eleventyConfig.setLibrary("md", markdownLib);

  // CSV template support
  eleventyConfig.addTemplateFormats("csv");
  eleventyConfig.addExtension("csv", {
    read: true,
    getData: async function(inputPath) {
      return {
        layout: "layouts/csv.njk",
        eleventyExcludeFromCollections: false
      };
    },
    getInstanceFromInputPath: function(inputPath) {
      return inputPath;
    },
    compile: function(inputContent, inputPath) {
      // Parse CSV to array of objects with relaxed parsing for malformed CSVs
      try {
        const records = parse(inputContent, {
          columns: true,
          skip_empty_lines: true,
          trim: true,
          relax_column_count: true,  // Allow inconsistent column counts
          relax_quotes: true,         // Allow quotes in unquoted fields
          escape: '"',
          quote: '"'
        });

        return function(data) {
          // Make CSV data available to template
          data.csvData = records;
          data.csvColumns = records.length > 0 ? Object.keys(records[0]) : [];

          // Return empty string - layout will render the content
          return "";
        };
      } catch (error) {
        console.warn(`Warning: Could not parse CSV file ${inputPath}:`, error.message);
        return function(data) {
          data.csvData = [];
          data.csvColumns = [];
          data.csvError = error.message;
          return "";
        };
      }
    },
    compileOptions: {
      permalink: function(data, inputPath) {
        const relativePath = inputPath.replace(/^.*users\/[^/]+\//, '').replace(/\.csv$/, '');
        return `/${relativePath}/index.html`;
      }
    },
    outputFileExtension: "html"
  });

  // JSON template support
  eleventyConfig.addTemplateFormats("json");
  eleventyConfig.addExtension("json", {
    read: true,
    getData: async function(inputPath) {
      return {
        layout: "layouts/json.njk",
        eleventyExcludeFromCollections: false
      };
    },
    getInstanceFromInputPath: function(inputPath) {
      return inputPath;
    },
    compile: function(inputContent, inputPath) {
      // Parse and format JSON
      try {
        const jsonData = JSON.parse(inputContent);
        const jsonFormatted = JSON.stringify(jsonData, null, 2);

        return function(data) {
          // Make JSON data available to template
          data.jsonData = jsonData;
          data.jsonFormatted = jsonFormatted;

          // Return empty string - layout will render the content
          return "";
        };
      } catch (error) {
        console.warn(`Warning: Could not parse JSON file ${inputPath}:`, error.message);
        return function(data) {
          data.jsonData = null;
          data.jsonFormatted = "";
          data.jsonError = error.message;
          return "";
        };
      }
    },
    compileOptions: {
      permalink: function(data, inputPath) {
        const relativePath = inputPath.replace(/^.*users\/[^/]+\//, '').replace(/\.json$/, '');
        return `/${relativePath}/index.html`;
      }
    },
    outputFileExtension: "html"
  });

  // Passthrough copy for specific file types (preserve directory structure)
  eleventyConfig.addPassthroughCopy(`../../users/${username}/**/*.{png,jpg,jpeg,gif,svg}`);

  // Ignore large files and virtual environments
  eleventyConfig.ignores.add(`../../users/${username}/**/*.{mp4,mov,avi,mkv,pdf,zip,tar,gz}`);
  eleventyConfig.ignores.add(`../../users/${username}/**/.venv/**/*`);

  // Custom filters
  eleventyConfig.addFilter("formatDate", function(date) {
    if (!date) return "";
    return new Date(date).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  });

  eleventyConfig.addFilter("dirname", function(filepath) {
    if (!filepath) return "";
    const parts = filepath.split('/');
    return parts.slice(0, -1).join('/');
  });

  eleventyConfig.addFilter("basename", function(filepath) {
    if (!filepath) return "";
    const parts = filepath.split('/');
    return parts[parts.length - 1];
  });

  eleventyConfig.addFilter("extension", function(filepath) {
    if (!filepath) return "";
    const match = filepath.match(/\.([^.]+)$/);
    return match ? match[1] : "";
  });

  eleventyConfig.addFilter("split", function(str, separator) {
    if (!str) return [];
    return str.split(separator);
  });

  eleventyConfig.addFilter("unique", function(arr) {
    return [...new Set(arr)];
  });

  eleventyConfig.addFilter("first", function(arr) {
    return arr && arr.length > 0 ? arr[0] : null;
  });

  eleventyConfig.addFilter("capitalize", function(str) {
    if (!str) return "";
    return str.charAt(0).toUpperCase() + str.slice(1);
  });

  eleventyConfig.addFilter("replace", function(str, search, replace) {
    if (!str) return "";
    return str.replace(new RegExp(search, 'g'), replace);
  });

  // Auto-discover collections from folder structure
  eleventyConfig.addCollection("allContent", function(collectionApi) {
    return collectionApi.getAll().filter(item => {
      return item.inputPath.includes(`users/${username}`);
    });
  });

  eleventyConfig.addCollection("workflows", function(collectionApi) {
    return collectionApi.getFilteredByGlob(`../../users/${username}/workflows/**/*.md`);
  });

  eleventyConfig.addCollection("outputs", function(collectionApi) {
    return collectionApi.getFilteredByGlob(`../../users/${username}/outputs/**/*.md`);
  });

  eleventyConfig.addCollection("byFolder", function(collectionApi) {
    const byFolder = {};
    const items = collectionApi.getAll().filter(item => {
      return item.inputPath.includes(`users/${username}`);
    });

    items.forEach(item => {
      const folder = item.inputPath.split('/').slice(0, -1).join('/');
      if (!byFolder[folder]) {
        byFolder[folder] = [];
      }
      byFolder[folder].push(item);
    });

    return byFolder;
  });

  // Add markdown files to their directories in the directories data
  eleventyConfig.addCollection("directoriesWithContent", function(collectionApi) {
    const directoriesDataPath = path.join(__dirname, 'templates', '_data', 'directories.js');
    const directories = require(directoriesDataPath)();
    const allMarkdown = collectionApi.getFilteredByGlob(`../../users/${username}/**/*.md`);

    // Map markdown files to their directories
    const userPathRegex = new RegExp(`^.*users/${username}/`);
    directories.forEach(dir => {
      dir.markdown = allMarkdown.filter(item => {
        const itemDir = item.inputPath
          .replace(userPathRegex, '')
          .split('/')
          .slice(0, -1)
          .join('/');
        return itemDir === dir.path;
      });
    });

    return directories;
  });

  // Build navigation tree from folder structure
  eleventyConfig.addGlobalData("navigationTree", function() {
    // Resolve from the directory where eleventy runs (sites/{username})
    const userDir = path.resolve(process.cwd(), '..', '..', 'users', username);

    function buildTree(dirPath, basePath = '') {
      const items = [];

      try {
        const entries = fs.readdirSync(dirPath, { withFileTypes: true });

        for (const entry of entries) {
          // Skip hidden files and certain directories
          if (entry.name.startsWith('.') || entry.name === 'node_modules' || entry.name === '_site') {
            continue;
          }

          const fullPath = path.join(dirPath, entry.name);
          const relativePath = basePath ? `${basePath}/${entry.name}` : entry.name;

          if (entry.isDirectory()) {
            const children = buildTree(fullPath, relativePath);

            items.push({
              type: 'folder',
              name: entry.name,
              path: relativePath,
              children: children
            });
          } else {
            // Only include supported file types
            const ext = path.extname(entry.name).slice(1);
            if (['md', 'csv', 'json'].includes(ext)) {
              const nameWithoutExt = path.basename(entry.name, path.extname(entry.name));
              const url = `/${relativePath.replace(/\.[^.]+$/, '')}/`;

              items.push({
                type: 'file',
                name: nameWithoutExt,
                path: relativePath,
                extension: ext,
                url: url
              });
            }
          }
        }
      } catch (error) {
        console.warn(`Warning: Could not read directory ${dirPath}:`, error.message);
      }

      // Sort: folders first, then files, both alphabetically
      items.sort((a, b) => {
        if (a.type !== b.type) {
          return a.type === 'folder' ? -1 : 1;
        }
        return a.name.localeCompare(b.name);
      });

      return items;
    }

    return buildTree(userDir);
  });

  // Add computed breadcrumb data for all pages
  eleventyConfig.addGlobalData("eleventyComputed", {
    breadcrumbHtml: (data) => {
      // Skip if no page URL or if it's the root
      if (!data.page || !data.page.url || data.page.url === '/') {
        return null;
      }

      const parts = data.page.url.split('/').filter(p => p);
      if (parts.length === 0) {
        return null;
      }

      let breadcrumb = '<a href="/">Home</a>';
      let currentPath = '';

      parts.forEach((part) => {
        currentPath += '/' + part;
        const formattedPart = part
          .replace(/-/g, ' ')
          .replace(/_/g, ' ')
          .replace(/\b\w/g, l => l.toUpperCase());
        breadcrumb += `<span>/</span> <a href="${currentPath}/">${formattedPart}</a>`;
      });

      return breadcrumb;
    }
  });

  return {
    dir: {
      input: `../../users/${username}`,
      output: `../../_site/${username}`,
      includes: "../../_eleventy/templates/_includes",
      data: "../../_eleventy/templates/_data"
    },
    templateFormats: ["md", "njk", "html", "csv", "json"],
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",
    dataTemplateEngine: false,
    pathPrefix: "/"
  };
};
