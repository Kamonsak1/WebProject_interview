function all_list(topics) {
    var item = document.getElementById('item');
    item.checked= false;
    var topicsArray = topics.split(','); // แยกสตริงเป็นอาร์เรย์

    var filteredTopics = topicsArray.filter(function(topic) {
        return topic.trim() !== '';
    });

    var container = document.getElementById('checkbox-container');
    container.innerHTML = '';

    filteredTopics.forEach(function(topic) {
        var parts = topic.split('-'); 
        var topicLabel = parts[0]; 
        var topicData = topic;

        var checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = topicData; 
        checkbox.value = topicData; 
        checkbox.name = 'checkbox'; 

        var label = document.createElement('label');
        label.htmlFor = topicData;
        label.appendChild(document.createTextNode(topicLabel));

        container.appendChild(checkbox);
        container.appendChild(label);
        container.appendChild(document.createElement('br'));
    });
}
