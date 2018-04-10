import React from "react";
import PropTypes from "prop-types";
import TextField from 'material-ui/TextField';


const TextFields = ({ field, label, value, error, onChange, type }) => {
    const has_error = error != undefined && error != '';
    return <div className="group">

        <TextField
            type={type}
            onChange={onChange}
            value={value}
            name={field}
            className="control"
            placeholder={label}
            error={has_error}
            helperText={error}

        />
    </div>;
};

TextFields.propTypes = {
    field: PropTypes.string.isRequired,
    value: PropTypes.string.isRequired,
    label: PropTypes.string.isRequired,
    type: PropTypes.string.isRequired,
    onChange: PropTypes.func.isRequired,
    error: PropTypes.string.isRequired
};

TextFields.defaultProps = {
    type: "text"
};

export default TextFields;
