//--- store

let store = {
  title: 'Yellow Deep',
  palettes: []
}

//--- load json

const getJson = url => {
  return (
    fetch(url, {
      method: 'get',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json'
      }
    })
      // return json
      .then(response => response.json())
      .catch(error => {
        console.error('fetch error:', url, error)
      })
  )
}

//--- header

const Header = () => <h1>{store.title}</h1>

//--- data display

class Palettes extends React.Component {
  constructor(props) {
    super(props)

    this.state = {}
  }

  componentDidMount() {
    // get palettes

    getJson('/palettes').then(json => {
      store.palettes = json.palettes
      renderPage()
    })
  }

  render() {
    return (
      <div className="palettes">
        {store.palettes.map(p => (
          <div key={p.id} className="palette">
            {p.colors.map(c => (
              <div
                key={c.id}
                style={{
                  backgroundColor: `hsl(${c.h * 360}, ${c.s * 100}%, ${c.l *
                    100}%)`
                }}
                className="palette-color"
              />
            ))}
          </div>
        ))}
      </div>
    )
  }
}
//--- app

const App = () => {
  return (
    <div>
      <Header />
      <Palettes />
    </div>
  )
}

//--- site render

// call this to render the site
const renderPage = () => {
  ReactDOM.render(<App />, document.getElementById('root'))
}

//--- app startup

renderPage()
