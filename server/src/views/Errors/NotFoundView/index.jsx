import React from "react";
import { Box, Container, Typography } from "@material-ui/core";
import Page from "src/components/Page";
import styles from "./styles.module.scss";
import withAuthentication from "src/hoc/withAuthentication";

const NotFoundView = () => {
  return (
    <Page className={styles.root} title="404">
      <Box
        display="flex"
        flexDirection="column"
        height="100%"
        justifyContent="center"
      >
        <Container maxWidth="md">
          <Typography align="center" color="textPrimary" variant="h1">
            The page you are looking for isn’t here!
          </Typography>
          <Typography align="center" color="textPrimary" variant="subtitle2">
            You either tried some shady route or you came here by mistake.
            Whichever it is, try using the navigation
          </Typography>
          <Box textAlign="center">
            <img
              alt="Under development"
              className={styles.image}
              src="/static/images/undraw_page_not_found_su7k.svg"
            />
          </Box>
        </Container>
      </Box>
    </Page>
  );
};

export default withAuthentication(NotFoundView);
