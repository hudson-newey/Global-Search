var getUrlParameter = function getUrlParameter(sParam) {
    let sPageURL = window.location.search.substring(1),
        sURLVariables = sPageURL.split('&'),
        sParameterName;

    sURLVariables.forEach((url) => {
        const sParameterNamec = url.split("=");
        if (sParameterNamec[0] === sParam)
            return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
    })
};
