let video = document.getElementById("video");
let canvas = document.getElementById("canvas");
let preview = document.getElementById("preview");
let cameraImage = document.getElementById("camera_image");
let loader = document.getElementById("loader");

function startCamera(){
    preview.style.display="none";
    video.style.display="block";

    navigator.mediaDevices.getUserMedia({video:true})
    .then(stream=>{
        video.srcObject=stream;
    });
}

function capture(){
    let context=canvas.getContext("2d");
    context.drawImage(video,0,0,300,300);

    let data=canvas.toDataURL("image/png");

    cameraImage.value=data;
    preview.src=data;

    video.style.display="none";
    preview.style.display="block";
}

function previewUpload(event){
    let file=event.target.files[0];

    if(file){
        let reader=new FileReader();

        reader.onload=function(e){
            preview.src=e.target.result;
            preview.style.display="block";
            video.style.display="none";
        }

        reader.readAsDataURL(file);
    }
}

function showLoader(){
    loader.style.display="block";
}