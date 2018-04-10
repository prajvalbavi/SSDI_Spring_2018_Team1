import validator from "validator";


export default function validateInput(data) {
    let errors = {};
    let isValid = true
    if (data.identifier == ''){
        errors.identifier = "Username is required";
        isValid = false;
    }

    if(data.password==''){
        errors.password = "Password is required";
        isValid = false;
    }

    return {
        errors,
        isValid
    };
}