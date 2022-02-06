/* third lib*/
import React, { useMemo } from "react";
import { useRoutes } from "react-router-dom";
import "react-perfect-scrollbar/dist/css/styles.css";
import { IntlProvider } from "react-intl";

/*local component & methods*/
import routes from "src/routes";
import "@assets/GlobalStyles.css";
import "@assets/comCover.scss";
import { useGlobalContext } from "src/context";

/* language config*/
import CN from "src/language/CN.js";
import US from "src/language/US.js";

const App = () => {
  const { languageContext } = useGlobalContext();
  const language = languageContext.lang;
  let routing = useRoutes(routes(language));
  const message = useMemo(() => {
    switch (language) {
      case "en":
        return US;
      case "cn":
        return CN;
      default:
        return US;
    }
  }, [language]);

  return (
    <IntlProvider messages={message} locale="fr" defaultLocale="en">
      {routing}
    </IntlProvider>
  );
};

export default App;
