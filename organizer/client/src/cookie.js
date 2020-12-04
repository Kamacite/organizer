export function setCookie(name, value, session=true) {
    let expire_date = new Date();
    expire_date.setFullYear(expire_date.getFullYear() + 1);
    if(session) {
        document.cookie = name + "=" + value;
    }
    else {
        document.cookie = name + "=" + value + ";expires=" + expire_date.toUTCString()
    }
    return true;
}

export function unsetCookie(name) {
    document.cookie = name + "=" + ";expires=Thu, 01 Jan 1970 00:00:01 GMT"
}

export function getCookie(name) {
    return document.cookie
            .split(';')
            .find(row => row.trim().startsWith(name))
            .split('=')[1];
}