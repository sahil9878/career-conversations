import GithubIcon from './assets/github-icon.tsx'
import './App.css'
import LinkedinIcon from './assets/linkedin-icon.tsx'
function App() {
  return (
    <main>
      <div
        className="background__pattern"
      />
      <section className="intro">
        <header>
          <h1>
            Sahil Singh
          </h1>
          <h2>Full-Stack Developer</h2>
          <p>
            Hi. I'm Sahil, a Software Engineer with a passion for building web applications and exploring new technologies.
            I enjoy solving complex problems and creating intuitive user interfaces.
          </p>
        </header>
        <nav>
          Let's get in touch!
          <ul>
            <li>
              <a href="https://www.linkedin.com/in/sahil-singh98/" target="_blank" >
                <LinkedinIcon height={24} width={24} />
                LinkedIn</a>
            </li>
            <li>
              <a href="https://github.com/sahil9878" target="_blank" >
                <GithubIcon height={24} width={24} />
                GitHub</a>
            </li>
          </ul>
        </nav>
      </section>
      <section className='conversation'>
        <p>
          Want to learn more about me? Ask my AI assistant!
        </p>
        <div className="chat-widget">
        </div>
      </section>
    </main>
  )
}

export default App
