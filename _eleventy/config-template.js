const syntaxHighlight = require("@11ty/eleventy-plugin-syntaxhighlight");
const markdownIt = require("markdown-it");
const markdownItAnchor = require("markdown-it-anchor");
const path = require("path");
const { parse } = require("csv-parse/sync");

module.exports = function(eleventyConfig, username) {
  // Plugins
  eleventyConfig.addPlugin(syntaxHighlight);

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

  // Passthrough copy for specific file types (preserve directory structure)
  eleventyConfig.addPassthroughCopy(`../../users/${username}/**/*.json`);
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

  return {
    dir: {
      input: `../../users/${username}`,
      output: `../../_site/${username}`,
      includes: "../../_eleventy/templates/_includes",
      data: "../../_eleventy/templates/_data"
    },
    templateFormats: ["md", "njk", "html", "csv"],
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",
    dataTemplateEngine: false,
    pathPrefix: "/"
  };
};
