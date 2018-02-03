function toggle() {
    var searchBar = document.getElementsByClassName('search')[0];

    if (searchBar.style.display !== 'none')
        searchBar.style.display = 'none';
    else
        searchBar.style.display = 'initial';
}

function convert(ts) {
    var utc = ts;
    var d = new Date(0);
    d.setUTCSeconds(utc);
    return d.toUTCString();
}

function load(url) {
    if (url !== null) {
    }
    else {
        throw new Error("No url provided");
    }

    return 0;
}

function poll()
{
    return false;
}