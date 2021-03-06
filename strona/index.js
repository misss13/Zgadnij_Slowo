var data 
$.getJSON('http://balalaika.ct8.pl/punkty.json', function(data) {
      new gridjs.Grid({
        columns: ["Numer indexu", "Punkty z 32 gier"],
        sort: true,
        search: true,
        data: data,
        style: {
          table: {
            border: '3px rgba(153, 142, 142, 0)'
          },
          th: {
            'background-color': 'rgba(224, 80, 80, 0.952)',
            color: '#fff',
            'border-bottom': '3px #ccc',
            'text-align': 'center'
          },
          td: {
            'background-color': 'rgba(53, 51, 51, 1)',
            color: '#fff',
            'text-align': 'center'
          },
          container : {
            'background-color': 'rgba(53, 51, 51, 1)',
            color: '#000',
          },
          search: {
            'background-color': 'rgba(53, 51, 51, 1)',
            color: '#000',
          }
        }
      }).render(document.getElementById("wrapper"));
});

$.getJSON('http://balalaika.ct8.pl/ilosc_gier_graczy.json', function(data) {
      new gridjs.Grid({
        columns: ["Numer indexu", "Ilosc odbytych gier"],
        sort: true,
        search: true,
        data: data,
        style: {
          table: {
            border: '3px rgba(153, 142, 142, 0)'
          },
          th: {
            'background-color': 'rgba(224, 80, 80, 0.952)',
            color: '#fff',
            'border-bottom': '3px #ccc',
            'text-align': 'center'
          },
          td: {
            'background-color': 'rgba(53, 51, 51, 1)',
            color: '#fff',
            'text-align': 'center'
          },
          container : {
            'background-color': 'rgba(53, 51, 51, 1)',
            color: '#000',
          },
          search: {
            'background-color': 'rgba(53, 51, 51, 1)',
            color: '#000',
          }
        }
      }).render(document.getElementById("Ilosc"));
});

$.getJSON('http://balalaika.ct8.pl/kolejka.json', function(data) {
      new gridjs.Grid({
        columns: ["Kolejka z oczekującymi graczami - Numer indexu"],
        data: data,
        style: {
          th: {
            'background-color': 'rgba(224, 80, 80, 0.952)',
            color: '#fff',
            'border-bottom': '3px #ccc',
            'text-align': 'center'
          },
          td: {
            'background-color': 'rgba(53, 51, 51, 1)',
            color: '#fff',
            'text-align': 'center'
          },
          container : {
            'background-color': 'rgba(53, 51, 51, 1)',
            color: '#000',
          }
        }
      }).render(document.getElementById("Kolejka"));
});

$.getJSON('http://balalaika.ct8.pl/punkty.z30rund.json', function(data) {
      new gridjs.Grid({
        columns: ["Numer indexu", "Ilosc punktów w 30 grach"],
        sort: true,
        search: true,
        data: data,
        style: {
          table: {
            border: '3px rgba(153, 142, 142, 0)'
          },
          th: {
            'background-color': 'rgba(224, 80, 80, 0.952)',
            color: '#fff',
            'border-bottom': '3px #ccc',
            'text-align': 'center'
          },
          td: {
            'background-color': 'rgba(53, 51, 51, 1)',
            color: '#fff',
            'text-align': 'center'
          },
          container : {
            'background-color': 'rgba(53, 51, 51, 1)',
            color: '#000',
          },
          search: {
            'background-color': 'rgba(53, 51, 51, 1)',
            color: '#000',
          }
        }
      }).render(document.getElementById("pomylka"));
});
//format na pythona TODO [["NR INDEXU", "PUNKTY"],[kol osoba]....]