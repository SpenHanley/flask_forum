function toggle()
{
    var searchBar = document.getElementsByClassName('search')[0]

    if (searchBar.style.display != 'none')
        searchBar.style.display = 'none'
    else
        searchBar.style.display = 'initial'
}

function convert(ts) {
    var utc = ts;
    var d = new Date(0);
    d.setUTCSeconds(utc);
    return d.toUTCString();
}

function limit(length, text) {
    var container = document.getElementById('content');
    return text.substring(0, length);
}