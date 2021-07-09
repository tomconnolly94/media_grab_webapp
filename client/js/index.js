//////////////////////////////////////////////////////////////////////
//
// filename: index.js
// author: Tom Connolly
// description: Contains controller functionality for the index.html
//
//////////////////////////////////////////////////////////////////////

function submitModifiedItem(item, itemIndex){
	console.log(item);

	var formattedBlackListTerms = [];

	item.blacklistTerms.forEach((blacklistTerm) => {
		formattedBlackListTerms.push(blacklistTerm.content)
	});

	var formattedItem = {
		"name": item.name.content,
		"typeSpecificData": {
			"latestSeason": Number(item.typeSpecificData.latestSeason.content),
			"latestEpisode": Number(item.typeSpecificData.latestEpisode.content)
		},
		"blacklistTerms": formattedBlackListTerms,
	}
	console.log(formattedItem);

	
	axios.put(`/MediaInfoRecord/${itemIndex}`, formattedItem).then((response) => {
		console.log(response);
	});
}


function loadMediaIndexJson() {
	axios.get(`/MediaInfoRecords`).then((response) => {

		var mediaInfoList = response.data["media"];

		mediaInfoList = reformatMediaIndexData(mediaInfoList);

		new Vue({
			el: '#mediaIndexContent',
			data() {
				return {
					content: mediaInfoList,
					modalVisible: false,
					confirmCloseModalFunction: null,
					modalText: null,
				}
			},
			methods: {
				makeFieldEditable: function (field){
					field.edit = true;
				},
				confirmItemEdit: function (item, editedField, itemIndex){
					editedField.edit = false;
					submitModifiedItem(item, itemIndex);
				},
				xButtonClicked: function (itemIndex) {
					axios.delete(`/MediaInfoRecord/${itemIndex}`).then((response) => {
						window.location.href = "/";
					});
				},
				showModal: function(confirmFunction, modalText){
					this.modalText = modalText;
					this.modalVisible = true;
					this.confirmCloseModalFunction = confirmFunction;
				},
				confirmCloseModal: function(){
					this.modalVisible = false;
					this.confirmCloseModalFunction();
				},
				cancelCloseModal: function(){
					this.modalVisible = false;
					console.log("cancelCloseModal() called.");
				},
				addNewBlacklistTerm: function(item){
					item.newPotentialBlacklistItem.edit = false;
					console.log("blacklistTerm added: ", item.newPotentialBlacklistItem.content);
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
			if(typeof item[key] === 'object'){
				var subItem = item[key];
				Object.keys(subItem).forEach(subKey => {
					addEditFieldToObject(subItem, subKey);
				});				
			}
			else{
				addEditFieldToObject(item, key);
			}			
		});

		item.newPotentialBlacklistItem = {
			edit: false,
			content: ""
		}
	});
	return mediaIndexData;
}

loadMediaIndexJson();


// register modal component
Vue.component("modal", {
	template: "#modal-template",
	methods:{
		okCloseModal: function(){
			console.log("Ok");
		},
		cancelCloseModal: function(){
			console.log("cancel");
		}
	}
});

new Vue({
	el: '#triggerPanel',
	data() {
		return {
			responseMessage: "",
			running: false,
			startTime: null
		}
	},
	methods: {
		runMediaGrab: function (){
			if (this.running){
				return;
			}

			this.running = true;
			this.startTime = new Date().toLocaleString();

			axios.get(`/runMediaGrab`).then((response) => {
				console.log("runMediaGrab successfully run");
				this.responseMessage = `MediaGrab run at ${this.startTime}`
				this.running = false;
			});
		}
	}
});