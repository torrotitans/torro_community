import moment from "moment-timezone";
import TIME_FORMAT from "src/lib/data/timeFormat";
const timeZone = "Asia/Hong_Kong";
const timeFormat = "ddd, DD MMM YYYY HH:mm:ss";

export const covertToCurrentTime = (date, zone) => {
  let currZone = zone || timeZone;
  let suffix = "";

  TIME_FORMAT.forEach((item) => {
    if (item.value === currZone) suffix = item.suffix;
  });
  return (
    moment(date)
      .tz(zone || timeZone)
      .format(timeFormat) + ` ${suffix}`
  );
};
