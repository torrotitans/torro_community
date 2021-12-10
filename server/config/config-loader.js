const fs = require("fs");
const path = require("path");

module.exports = function configLoader(source) {
  if (process.env.REACT_APP_ENV && !/[?&]raw=true/.test(this.resourceQuery)) {
    const dirName = path.dirname(this.resourcePath);
    const baseName = path.basename(this.resourcePath);
    const resourcePath = path.resolve(
      dirName,
      process.env.REACT_APP_ENV,
      baseName
    );

    if (fs.existsSync(resourcePath)) {
      this.addDependency(resourcePath);
      if (/\.json$/.test(baseName)) {
        return JSON.stringify(JSON.parse(fs.readFileSync(resourcePath)));
      }

      return `module.exports = require('./${process.env.REACT_APP_ENV}/${baseName}?raw=true');`;
    }
  }

  return source;
};
