//--- header

const Header = () => <h1>Yellow Deep</h1>

//--- data display

class Palettes extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      palettes: [],
      selectedOnly: false,
      data: 'new'
    }

    this.getData = this.getData.bind(this)
    this.getJson = this.getJson.bind(this)
    this.updateSelection = this.updateSelection.bind(this)
  }

  componentDidMount() {
    // get palettes
    this.getData(this.state.data)
  }

  //--- load json

  getJson = (url, data) => {
    return (
      fetch(`${url}?data=${data}`, {
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

  // get new data when radio button changed

  getData = data => {
    this.setState({ data })

    this.getJson('/palettes', data).then(json => {
      this.setState({ palettes: json.palettes })
    })
  }
  //--- post selection

  updateSelection = data => {
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

  render() {
    return (
      <div>
        <div className="options-container no-print">
          <div>
            <input
              id="selected-only"
              type="checkbox"
              value="selected-only"
              checked={this.state.selectedOnly}
              onChange={() => {
                this.setState({ selectedOnly: !this.state.selectedOnly })
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
              checked={this.state.data === 'training'}
              onChange={e => {
                this.getData(e.target.value)
              }}
            />
            <label htmlFor="data-training">Training</label>
            <input
              id="data-new"
              type="radio"
              value="new"
              checked={this.state.data === 'new'}
              onChange={e => {
                this.getData(e.target.value)
              }}
            />
            <label htmlFor="data-new">Test</label>
          </div>
        </div>
        <div className="selections-count">
          {this.state.palettes.filter(p => p.selected).length} selections out of{' '}
          {this.state.palettes.length}
        </div>
        <div
          className={`palettes ${
            this.state.selectedOnly ? 'selected-only' : ''
          }`}
        >
          {this.state.palettes.map(
            (p, i) =>
              (!this.state.selectedOnly || p.selected) && (
                <button
                  key={p.id}
                  className={`palette ${p.selected ? 'selected' : ''}`}
                  onClick={() => {
                    p.selected = !p.selected
                    this.updateSelection({ id: p.id })
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
