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
            You do not have any workspace access!
          </Typography>
          <Typography align="center" color="textPrimary" variant="subtitle2">
            Please contact your IT support.
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
