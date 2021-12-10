export default (value, option) => {
  let valueStr = "";
  let valueList = value.split(",");
  option.forEach((item, index) => {
    let label = item.label;
    if (valueList[index] === "true") {
      valueStr += index === option.length - 1 ? `${label}` : `${label}, `;
    }
  });
  return valueStr;
};
