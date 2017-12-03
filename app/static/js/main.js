function toggle()
{
    var searchBar = document.getElementsByClassName('search')[0]

    if (searchBar.style.display != 'none')
        searchBar.style.display = 'none'
    else
        searchBar.style.display = 'initial'
}