/* third lib */
import React from "react";
import PropTypes from "prop-types";
import cn from "classnames";

/* material-ui */
import Paper from "@material-ui/core/Paper";
import InputBase from "@material-ui/core/InputBase";
import IconButton from "@material-ui/core/IconButton";
import SearchIcon from "@material-ui/icons/Search";

/* local components & methods */
import styles from "./styles.module.scss";

const Search = ({ value, onChange, handleSearch, fullWidth, placeholder }) => {
  return (
    <Paper className={cn(styles.search, { [styles["fullWidth"]]: fullWidth })}>
      <InputBase
        className={styles.input}
        placeholder={placeholder}
        inputProps={{ "aria-label": "search google maps" }}
        defaultValue={value}
        onChange={(e) => {
          onChange(e.target.value);
        }}
        startAdornment={
          <IconButton
            type="submit"
            className={styles.iconButton}
            aria-label="search"
            onClick={handleSearch}
          >
            <SearchIcon />
          </IconButton>
        }
      />
    </Paper>
  );
};

Search.propTypes = {
  onChange: PropTypes.func,
};

export default Search;
