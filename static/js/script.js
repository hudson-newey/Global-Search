$(document).ready(function() {
    let searchTerm = getUrlParameter('q').replace('+', ' ');;
    document.title = searchTerm + " at Global Search";
    $("#searchBox").val(searchTerm);
});