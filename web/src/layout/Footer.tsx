// Pagine legali statiche (HTML del sito), non rotte dell'app: link assoluti, non <Link>.
const LEGALI = [
  { href: '/disclaimer.html', label: 'Disclaimer' },
  { href: '/privacy-policy.html', label: 'Privacy' },
  { href: '/cookie-policy.html', label: 'Cookie' },
]

export function Footer() {
  return (
    <footer className="border-border text-muted-foreground border-t py-8 text-sm">
      <div className="ch-wrap flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <p>Frequenze descrittive su dati gia' visti, non segnali.</p>
        <ul className="flex gap-4">
          {LEGALI.map((l) => (
            <li key={l.href}>
              <a href={l.href} className="hover:text-foreground underline-offset-4 hover:underline">
                {l.label}
              </a>
            </li>
          ))}
        </ul>
      </div>
    </footer>
  )
}
