/* Schakelwerk component canvas — mount */

const { createRoot } = ReactDOM;

function App() {
  return (
    <DesignCanvas>
      <SEC.Foundations/>
      <SEC.Primitives/>
      <SEC.Status/>
      <SEC.Forms/>
      <SEC.Data/>
      <SEC.Feedback/>
      <SEC.Overlays/>
      <SEC.Layout/>
      <SEC.Composites/>
      <SEC.BuildFirst/>
    </DesignCanvas>
  );
}

const root = createRoot(document.getElementById("root"));
root.render(<App/>);
