import axios from 'axios'

export default function setAuthorizationToken (token){
    if(token) {
        axios.defaults.headers.common['Authorization'] = token;
        console.log("Auth token", axios.defaults.headers.common['Authorization'] )
    }else{
        delete axios.defaults.headers.common['Authorization']
    }
}
