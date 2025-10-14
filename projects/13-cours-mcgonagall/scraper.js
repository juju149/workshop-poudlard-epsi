import puppeteer from 'puppeteer';
import { execSync } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { readFileSync, existsSync } from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Charger .env si ce n'est pas déjà fait (pour compatibilité avec asar)
const envPath = join(__dirname, '.env');
if (existsSync(envPath) && !process.env.USERNAME) {
  const envContent = readFileSync(envPath, 'utf8');
  envContent.split('\n').forEach(line => {
    const match = line.match(/^([^=:#]+)=(.*)$/);
    if (match) {
      const key = match[1].trim();
      const value = match[2].trim().replace(/^["']|["']$/g, '');
      if (!process.env[key]) {
        process.env[key] = value;
      }
    }
  });
}

// Trouve le chemin de Chrome/Chromium sur le système
function findChrome() {
  const paths = [
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Chromium.app/Contents/MacOS/Chromium',
    '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
  ];
  
  for (const path of paths) {
    try {
      execSync(`test -f "${path}"`, { stdio: 'ignore' });
      return path;
    } catch (e) {
      // Continue
    }
  }
  
  // Si aucun Chrome trouvé, utiliser celui de Puppeteer
  return null;
}

async function scrapeSchedule(date = null) {
  const chromePath = findChrome();
  const launchOptions = { 
    headless: false,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  };
  
  if (chromePath) {
    launchOptions.executablePath = chromePath;
  }
  
  const browser = await puppeteer.launch(launchOptions);
  let result;
  try {
    const page = await browser.newPage();
    // Format de la date : JJ/MM/AAAA (fr-FR)
    const targetDate = date || new Date().toLocaleDateString('fr-FR');
    const username = process.env.USERNAME;
    const url = `https://ws-edt-cd.wigorservices.net/WebPsDyn.aspx?action=posEDTLMS&serverID=C&Tel=${username}&date=${targetDate}`;
    await page.goto(url);

    // Connexion automatique si la page de login est détectée
    if (await page.$('#fm1')) {
      console.log('Page de connexion détectée, tentative de login...');
      await page.waitForSelector('#username', {visible: true});
      await page.waitForSelector('#password', {visible: true});
      await page.type('#username', username);
      await page.type('#password', process.env.PASSWORD);
      await page.click('#submitBtn');
      // Attente de l'apparition du planning après login
      try {
        await page.waitForSelector('.Jour', {timeout: 60000});
        console.log('Login effectué et planning chargé.');
      } catch (err) {
        console.error('Erreur : le planning n\'a pas chargé après le login. Vérifiez vos identifiants ou la page cible.');
        throw err;
      }
    }

    // Récupère tous les cours par jour avec la logique corrigée
    result = await page.evaluate(() => {
      const days = Array.from(document.querySelectorAll('.Jour'));
      return days.map(day => {
        // Récupère la date du jour
        const date = day.querySelector('.TCJour')?.textContent?.trim();
        
        // Récupère la position left du jour
        const dayLeft = parseFloat(day.style.left);
        
        // Trouve tous les éléments .Case ayant une position left similaire
        const cases = Array.from(document.querySelectorAll('.Case')).filter(c => {
          const caseLeft = parseFloat(c.style.left);
          // Tolérance de 1% pour compenser les arrondis
          return Math.abs(caseLeft - dayLeft) < 1;
        });
        
        // Extrait les infos de chaque cours
        const cours = cases.map(c => {
          const table = c.querySelector('table.TCase');
          if (!table) return null;
          
          const rows = table.querySelectorAll('tr');
          if (rows.length < 3) return null;
          
          // Matière (première ligne)
          const matiere = rows[0]?.querySelector('.TCase')?.textContent?.trim() || '';
          
          // Prof et informations (deuxième ligne)
          const profInfo = rows[1]?.querySelector('.TCProf');
          let prof = '';
          if (profInfo) {
            const html = profInfo.innerHTML || '';
            // Prendre le texte avant le premier <br>
            prof = html.split('<br>')[0].replace(/<[^>]*>/g, '').replace(/\s+/g, ' ').trim();
          }
          
          // Heure et salle (troisième ligne)
          const heure = rows[2]?.querySelector('.TChdeb')?.textContent?.trim() || '';
          const salle = rows[2]?.querySelector('.TCSalle')?.textContent?.trim() || '';
          
          return {
            matiere: matiere.replace(/\s+/g, ' '),
            prof: prof,
            heure: heure,
            salle: salle.replace('Salle:', '').trim()
          };
        }).filter(Boolean);
        
        return { date, cours };
      }).filter(day => day.cours.length > 0); // Ne garde que les jours avec des cours
    });
  } catch (err) {
    await browser.close();
    process.exit(1);
    throw err;
  }
  await browser.close();
  return result;
}

export { scrapeSchedule };
