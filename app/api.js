import Constants from 'expo-constants';
const REPORT_URL = "http://m.bbarwik.com/a11y/api.php";

// TODO: Use Advanced API instead os simple API, also error handling

class API {
    send = async (data) => {
        data.session = Constants.sessionId;
        while(true) {
            let request = await fetch(REPORT_URL, {
                method: 'POST',
                headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });
            if(request.status == 200) {
                break;
            }
        }
    }
}

export default new API();