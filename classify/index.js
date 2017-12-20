//--- store

let store = {
  title: 'Yellow Deep',
  palettes: [],
  selectedOnly: false,
  data: 'training'
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
    fetch('/update-selection', {
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

    getJson('/palettes?data=train').then(json => {
      store.palettes = json.palettes
      renderPage()
    })
  }

  render() {
    return (
      <div>
        <div className="options-container no-print">
          <div>
            <input
              id="selected-only"
              type="checkbox"
              value="selected-only"
              checked={store.selectedOnly}
              onChange={() => {
                store.selectedOnly = !store.selectedOnly
                renderPage()
              }}
            />
            <label htmlFor="selected-only">Selected only</label>
          </div>
          <div>
            {/* data type */}
            Data :
            <input
              id="data-training"
              type="radio"
              value="training"
              checked={store.selectedOnly}
              onChange={() => {
                store.data = e.target.value

                renderPage()
              }}
            />
            <label htmlFor="data-training">Training</label>
            <input
              id="data-new"
              type="radio"
              value="new"
              checked={store.selectedOnly}
              onChange={e => {
                store.data = e.target.value

                renderPage()
              }}
            />
            <label htmlFor="data-new">New</label>
          </div>
        </div>
        <div className="selections-count">
          {store.palettes.filter(p => p.selected).length} selections out of{' '}
          {store.palettes.length}
        </div>
        <div
          className={`palettes ${store.selectedOnly ? 'selected-only' : ''}`}
        >
          {store.palettes.map(
            (p, i) =>
              (!store.selectedOnly || p.selected) && (
                <button
                  key={p.id}
                  className={`palette ${p.selected ? 'selected' : ''}`}
                  onClick={() => {
                    p.selected = !p.selected
                    updateSelection({ id: p.id })
                    renderPage()
                  }}
                >
                  <div className="palette-container">
                    {p.colors.map(c => (
                      <div
                        key={c.id}
                        style={{
                          backgroundColor: `hsl(${c.h * 360}, ${c.s *
                            100}%, ${c.l * 100}%)`
                        }}
                        className="palette-color"
                      />
                    ))}
                    <h2 className="no-print">{i + 1}</h2>
                  </div>
                </button>
              )
          )}
        </div>
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
