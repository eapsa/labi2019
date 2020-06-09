
	function PreverIMG() {
 
		var oFReader = new FileReader();
		oFReader.readAsDataURL(document.getElementById("img").files[0]);
 
		oFReader.onload = function (oFREvent) {
 
			document.getElementById("UploadPreVer").src = oFREvent.target.result;
 
		};
	};
 
