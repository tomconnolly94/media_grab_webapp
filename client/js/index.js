//////////////////////////////////////////////////////////////////////
//
// filename: index.js
// author: Tom Connolly
// description: Contains controller functionality for the index.html
//
//////////////////////////////////////////////////////////////////////

function updateMediaInfoName(recordName, newName){
	console.log(recordName);
	console.log(newName);
}

function updateMediaInfoLatestSeason(recordName, newLatestSeason){
	console.log(recordName);
	console.log(newLatestSeason);	
}

function updateMediaInfoLatestEpisode(recordName, newLatestEpisode){
	console.log(recordName);
	console.log(newLatestEpisode);
}

function updateMediaInfoBlacklistTerms(recordName, newBlacklist){
	console.log(recordName);
	console.log(newBlacklist);
}

var fieldHandlerMap = {
	"name": updateMediaInfoName,
	"latestSeason": updateMediaInfoLatestSeason,
	"latestEpisode": updateMediaInfoLatestEpisode,
	"blacklistTerms": updateMediaInfoBlacklistTerms
}

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
		"blacklistTerms": formattedBlackListTerms
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
					temp:"helloboi"
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
				xButtonClicked: function (recordName) {
					axios.delete(`/MediaInfoRecord?recordName=${recordName}`).then((response) => {
						window.location.href = "/";
					});
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
	});
	return mediaIndexData;
}

loadMediaIndexJson();