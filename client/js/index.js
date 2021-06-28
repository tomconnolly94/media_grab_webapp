Vue.directive('clickaway', {
	bind(el, { value }) {
		if (typeof value !== 'function') {
			console.warn(`Expect a function, got ${value}`)
			return
		}

		document.addEventListener('click', e => el.contains(e.target) || value())
	}
});

function loadMediaIndexJson() {
	axios.get(`/MediaIndex`).then((response) => {

		var mediaInfoList = response.data["media"];

		mediaInfoList = reformatMediaIndexData(mediaInfoList);

		new Vue({
			el: '#mediaIndexContent',
			data() {
				return {
					content: mediaInfoList
				}
			},
			methods: {
				xButtonClicked: function (recordName) {
					axios.delete(`/MediaInfoRecord?recordName=${recordName}`).then((response) => {
						window.location.href = "/";
					});
				},
				inputConfirmed: function(item, changedFieldName){
					console.log(item);
					console.log(changedFieldName);
				}
			}
		})
	});
}


function addEditFieldToObject(obj, relevantKey){

	var newObj = {
		edit: false
	}
	newObj["content"] = obj[relevantKey];

	obj[relevantKey] = newObj;
}


function reformatMediaIndexData(mediaIndexData) {
	mediaIndexData.forEach(item => {
		Object.keys(item).forEach(key => {
			if(Object.prototype.toString.call(item[key]) === '[object Object]'){
				var subItem = item[key];
				Object.keys(subItem).forEach(subKey => {
					addEditFieldToObject(subItem, subKey);
				});				
			}
			else{
				addEditFieldToObject(item, key);
			}			
		});
	});
	return mediaIndexData;
}

loadMediaIndexJson();