

function loadMediaIndexJson(){
  axios.get(`/MediaIndex`).then((response) => {

    var mediaIndexList = response.data["media"];

    // for(var i = 0; i < mediaIndexList.length; i++){
    //   mediaIndexList[i]["showBeingReleased"] = mediaIndexList["typeSpecificData"]["latestEpisode"] != 1;
    // }

    new Vue({
      el : '#mediaIndexContent',
      data () { 
        return {
          content: mediaIndexList
        } 
      }
    }) 
  });
}

loadMediaIndexJson();