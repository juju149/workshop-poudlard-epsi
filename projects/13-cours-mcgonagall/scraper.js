require('dotenv').config();
const puppeteer = require('puppeteer');

async function scrapeSchedule(date = null) {
  const browser = await puppeteer.launch({ headless: false });
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
      await browser.close();
      process.exit(1);
    }
  }

  // Récupère tous les cours par jour avec la logique corrigée
  const result = await page.evaluate(() => {
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
        const prof = profInfo ? profInfo.textContent?.replace(/\s+/g, ' ').trim() : '';
        
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

  await browser.close();
  
  return result;
}

// Utilisation : node scraper.js 10/13/2025
const inputDate = process.argv[2];
scrapeSchedule(inputDate);