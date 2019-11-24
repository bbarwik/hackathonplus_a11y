import Constants from 'expo-constants';
const REPORT_URL = "http://m.bbarwik.com/a11y/api.php";

class API {
    send = (data) => {
        data.session = Constants.sessionId;
        fetch(REPORT_URL, {
            method: 'POST',
            headers: {
              Accept: 'application/json',
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
          });
    }
}

export default new API();