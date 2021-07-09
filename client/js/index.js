//////////////////////////////////////////////////////////////////////
//
// filename: index.js
// author: Tom Connolly
// description: Contains controller functionality for the index.html
//
//////////////////////////////////////////////////////////////////////

var homeUrl = "/"

function submitModifiedItem(item, itemIndex, successCallback){

	var formattedItem = formatFrontendItemToBackendItem(item);
	
	axios.put(`/MediaInfoRecord/${itemIndex}`, formattedItem).then((response) => {
		successCallback();
	})
    .catch(err => {
    	console.log(err);
    });
}

function formatFrontendItemToBackendItem(frontendItem){
	
	//deal with formatting each blacklist term
	var formattedBlackListTerms = [];

	frontendItem.blacklistTerms.forEach((blacklistTerm) => {
		formattedBlackListTerms.push(blacklistTerm.content);
	});

	//deal with new a blacklist term, if it exists
	if(frontendItem.newPotentialBlacklistItem.content.length > 0){
		formattedBlackListTerms.push(frontendItem.newPotentialBlacklistItem.content);
	}

	var formattedItem = {
		"name": frontendItem.name.content,
		"typeSpecificData": {
			"latestSeason": Number(frontendItem.typeSpecificData.latestSeason.content),
			"latestEpisode": Number(frontendItem.typeSpecificData.latestEpisode.content)
		},
		"blacklistTerms": formattedBlackListTerms,
	};

	return formattedItem;
}


function loadMediaIndexJson() {
	axios.get(`/MediaInfoRecords`).then((response) => {

		var mediaInfoList = response.data["media"];

		mediaInfoList = formatBackendItemToFrontendItem(mediaInfoList);

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
					submitModifiedItem(item, itemIndex, function(){
						window.location.href = homeUrl;
					});
				},
				xButtonClicked: function (itemIndex) {
					axios.delete(`/MediaInfoRecord/${itemIndex}`).then((response) => {
						window.location.href = homeUrl;
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
				addNewBlacklistTerm: function(item, itemIndex){
					submitModifiedItem(item, itemIndex, function(){
						window.location.href = homeUrl;
					});
				}
			}
		});
	});
}


function addEditFieldToObject(obj, relevantKey){

	var newObj = {
		edit: false
	}
	newObj["content"] = obj[relevantKey];

	obj[relevantKey] = newObj;
}


function formatBackendItemToFrontendItem(mediaInfoData) {
	mediaInfoData.forEach(item => {
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
	return mediaInfoData;
}


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


// js execute section
loadMediaIndexJson();