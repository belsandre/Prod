module.exports = {
  layout: (data) => {
    // If no layout is already set and this is a markdown file, use page layout
    if (!data.layout && data.page.inputPath.endsWith('.md')) {
      return 'layouts/page.njk';
    }
    // Otherwise keep whatever layout is set (or undefined)
    return data.layout;
  }
};
