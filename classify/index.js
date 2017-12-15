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

//--- post selection

const updateSelection = data => {
  return (
    fetch('/updateselection', {
      method: 'post',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
      // return json
      .then(response => response.json())
      .catch(error => {
        console.error('fetch error:', error)
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
          <button
            key={p.id}
            className={`palette ${p.selected ? 'selected' : ''}`}
            onClick={() => {
              p.selected = !p.selected
              updateSelection({ id: p.id })
              renderPage()
            }}
          >
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
          </button>
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
