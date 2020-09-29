app.activeViewer.setActive();
var activeComp = app.project.activeItem;

var layers = app.project.activeItem.selectedLayers;

if(canWriteFiles())
{
    if (layers.length > 0)
    {
    var path = new File("My Sync").saveDlg(["Save Velo"],["VELO Files:*.velo"]);    
        
    var selected_layer = layers[0]
    var start_frame = selected_layer.inPoint * activeComp.frameRate
    var end_frame = selected_layer.outPoint * activeComp.frameRate

    var json = "{\r\n"

    for (var i = start_frame; i < end_frame; i++)
    {
            var current_time = i / activeComp.frameRate
            var time = selected_layer.property("Time Remap").valueAtTime(current_time, true)
            var frame = Math.floor(time * selected_layer.source.frameRate)
            $.writeln(frame)
            json = json + "\t\"" + i + "\": " + frame
            if(i < end_frame-1){
                json += ",\r\n"
                }
            
    }

    json += "\r\n}"


    $.writeln(json)
    $.writeln(path)
    //copyToClipboard(json)
    
    writeFile(path, json)
    

    //alert(time * selected_layer.source.frameRate)
    }else{
    alert ("No layers selected.");
    }
}

function writeFile(fileObj, fileContent, encoding) {

    encoding = encoding || "utf-8";
    fileObj = (fileObj instanceof File) ? fileObj : new File(fileObj);
    var parentFolder = fileObj.parent;
    if (!parentFolder.exists && !parentFolder.create())
        throw new Error("Cannot create file in path " + fileObj.fsName);
        
    fileObj.encoding = encoding;
    fileObj.open("w");
    fileObj.write(fileContent);
    fileObj.close();
    return fileObj;

}

function canWriteFiles() {

    if (isSecurityPrefSet()) return true;

    alert(script.name + " requires access to write files.\n" +

        "Go to the \"General\" panel of the application preferences and make sure " +

        "\"Allow Scripts to Write Files and Access Network\" is checked.");

    app.executeCommand(2359);

    return isSecurityPrefSet();

    function isSecurityPrefSet() {

        return app.preferences.getPrefAsLong(

            "Main Pref Section",

            "Pref_SCRIPTING_FILE_NETWORK_SECURITY"

        ) === 1;

    }

}

function copyToClipboard(string) {
	var cmd, isWindows;

	string = (typeof string === 'string') ? string : string.toString();
	isWindows = $.os.indexOf('Windows') !== -1;
	
	cmd = 'echo "' + string + '" | pbcopy';
	if (isWindows) {
		cmd = 'cmd.exe /c cmd.exe /c "echo ' + string + ' | clip"';
	}

	system.callSystem(cmd);
}


