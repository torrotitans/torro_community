export const STATIC_TEMPLATE = [
  {
    style: 1,
    default: {
      style: 1,
      label: "CheckBox",
      default: "",
      options: [{ label: "true" }, { label: "false" }],
    },
  },
  {
    style: 2,
    default: {
      style: 2,
      label: "Dropdown",
      default: "",
      options: [
        { label: "Option1", value: "Option1" },
        { label: "Option2", value: "Option2" },
      ],
    },
  },
  {
    style: 3,
    default: {
      style: 3,
      label: "Text",
      placeholder: "",
      default: "",
    },
  },
  {
    style: 4,
    default: {
      style: 4,
      label: "Upload",
      placeholder: "",
      default: "",
      multiple: false,
    },
  },
  {
    style: 5,
    default: {
      style: 5,
      label: "Switch",
      default: true,
      placeholder: "",
    },
  },
  {
    style: 6,
    default: {
      style: 6,
      label: "DatePicker",
      placeholder: "",
      default: "",
    },
  },
];
