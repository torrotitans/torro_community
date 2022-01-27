export default (value, option) => {
  let valueStr = "";
  option.forEach((item, index) => {
    if (item.value === value) {
      valueStr = item.label;
    }
  });
  return valueStr;
};
