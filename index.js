let store = {
  title: 'Yellow Deep'
};

//--- header

const Header = () => <h1>{store.title}</h1>;

//--- app

const App = () => {
  return <Header />;
};

//--- site render

// call this to render the site
const renderPage = () => {
  ReactDOM.render(<App />, document.getElementById('root'));
};

//--- app startup

renderPage();
