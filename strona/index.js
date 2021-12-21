var data 
$.getJSON('http://balalaika.ct8.pl/punkty.json', function(data) {
      new gridjs.Grid({
        columns: ["Numer indexu", "Punkty"],
        sort: true,
        data: data,
        style: {
          table: {
            border: '1px solid #ccc'
          },
          th: {
            'background-color': 'rgba(255, 0, 0, 0.1)',
            color: '#000',
            'border-bottom': '3px solid #ccc',
            'text-align': 'center'
          },
          td: {
            'text-align': 'center'
          }
        }
      }).render(document.getElementById("wrapper"));
});

$.getJSON('http://balalaika.ct8.pl/kolejka.json', function(data) {
      new gridjs.Grid({
        columns: ["Kolejka z oczekującymi graczami - Nrumer indexu"],
        data: data,
        style: {
          table: {
            border: '1px solid #ccc'
          },
          th: {
            'background-color': 'rgba(255, 0, 0, 0.1)',
            color: '#000',
            'border-bottom': '3px solid #ccc',
            'text-align': 'center'
          },
          td: {
            'text-align': 'center'
          }
        }
      }).render(document.getElementById("Kolejka"));
});

//format na pythona TODO [["NR INDEXU", "PUNKTY"],[kol osoba]....]