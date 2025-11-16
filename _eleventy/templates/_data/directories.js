const fs = require('fs');
const path = require('path');

module.exports = function() {
  const username = process.env.SITE_USERNAME || "user";
  const userDir = path.join(__dirname, '..', '..', '..', 'users', username);

  const directories = [];

  function scanDirectory(dir, relativePath = "") {
    try {
      const items = fs.readdirSync(dir);
      const folders = [];
      const files = [];
      let hasMarkdown = false;

      items.forEach(item => {
        // Skip hidden files and special directories
        if (item.startsWith('.') || item.startsWith('_') || item === 'node_modules') {
          return;
        }

        const fullPath = path.join(dir, item);
        const stats = fs.statSync(fullPath);

        if (stats.isDirectory()) {
          folders.push(item);
          // Recursively scan subdirectories
          const subPath = relativePath ? `${relativePath}/${item}` : item;
          scanDirectory(fullPath, subPath);
        } else if (stats.isFile()) {
          const ext = path.extname(item).toLowerCase();
          // Check for markdown files
          if (ext === '.md') {
            hasMarkdown = true;
          }
          // Only include specific file types (not markdown, as that's handled separately)
          if (['.json', '.csv', '.png', '.jpg', '.jpeg', '.gif', '.svg'].includes(ext)) {
            files.push({
              name: item,
              path: relativePath ? `${relativePath}/${item}` : item,
              url: `/${relativePath}/${item}`.replace(/\/+/g, '/'),
              size: formatFileSize(stats.size)
            });
          }
        }
      });

      // Add directory if it has content (folders, files, or markdown)
      if (folders.length > 0 || files.length > 0 || hasMarkdown) {
        directories.push({
          name: relativePath ? path.basename(relativePath) : username,
          path: relativePath || "",
          fullPath: dir,
          folders: folders,
          files: files,
          markdown: [] // Will be populated by collections
        });
      }
    } catch (err) {
      console.warn(`Warning: Could not scan directory ${dir}:`, err.message);
    }
  }

  function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  }

  scanDirectory(userDir);

  // Ensure root directory (path = "") is always first in the array
  directories.sort((a, b) => {
    if (a.path === '') return -1;
    if (b.path === '') return 1;
    return 0;
  });

  return directories;
};
