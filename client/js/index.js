

function loadMediaIndexJson(){
  axios.get(`/MediaIndex`).then((response) => {

    var mediaIndexList = response.data["media"];

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