image = ''

if (new URLSearchParams(window.location.search).get('reload') == "True") {
    console.log('reloaded!');
    image = document.getElementById("execute-button").src;
    image_split = image.split("/");
    image_name = image_split[image_split.length - 1];
    new_image_name = image.replace(image_name, 'reloaded_button.svg');
    console.log(new_image_name);
    document.getElementById("execute-button").src = new_image_name;
    setTimeout(function() { document.getElementById("execute-button").src = image; }, 1000);
};