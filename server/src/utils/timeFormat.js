import moment from "moment-timezone";

const timeZone = "Asia/Shanghai";
const timeFormat = "ddd, DD MMM YYYY HH:mm:ss";

export const covertToHKTime = (date) => {
  return (
    moment(date)
      .tz(timeZone)
      .format(timeFormat) + " (HKT)"
  );
};
