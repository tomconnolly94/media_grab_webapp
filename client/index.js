

function loadMediaIndexJson(){
  axios.get(`/MediaIndex`).then((response) => {

    var mediaIndexList = response.data["media"];
    zeroName = mediaIndexList[0].name;

    new Vue({
      el : '#MediaIndexContent',
      data () { 
        return {
          content: zeroName
        } 
      }
    }) 
  });
}

loadMediaIndexJson();