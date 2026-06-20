/**
 * Contact info formatting.
 *
 * Shared logic for turning a raw contact value (LinkedIn handle/URL, GitHub,
 * ORCID, website, email, phone, location) into a link href and a clean display
 * label. Mirrors the resume header so the cover letter letterhead can render
 * contact info identically.
 */

export type ContactLabel =
  | 'Email'
  | 'Phone'
  | 'Location'
  | 'Website'
  | 'LinkedIn'
  | 'GitHub'
  | 'ORCID';

export interface FormattedContact {
  /** Resolved link target (empty when not a link). */
  href: string;
  /** Cleaned, human-friendly text to display next to the icon. */
  displayText: string;
  /** Whether the value should render as a clickable link. */
  isLink: boolean;
}

/**
 * Format a single contact value for display.
 *
 * @param label - The kind of contact field.
 * @param value - The raw value as entered by the user.
 * @param hrefPrefix - Optional prefix for plain fields (e.g. `mailto:`, `tel:`).
 */
export function formatContact(
  label: ContactLabel,
  value: string,
  hrefPrefix: string = ''
): FormattedContact {
  let href = '';
  let displayText: string = value;
  let isLink = false;

  if (label === 'LinkedIn') {
    const clean = value.replace(/^https?:\/\/(?:www\.)?/, '');
    href = clean.includes('linkedin.com') ? `https://${clean}` : `https://linkedin.com/in/${clean}`;
    const match = href.match(/linkedin\.com\/in\/([^/?#\s]+)/);
    displayText = match ? match[1] : clean;
    isLink = true;
  } else if (label === 'GitHub') {
    const clean = value.replace(/^https?:\/\/(?:www\.)?/, '');
    href = clean.includes('github.com') ? `https://${clean}` : `https://github.com/${clean}`;
    const match = href.match(/github\.com\/([^/?#\s]+)/);
    displayText = match ? match[1] : clean;
    isLink = true;
  } else if (label === 'ORCID') {
    const cleanId = value
      .replace(/^https?:\/\/(?:www\.)?orcid\.org\//, '')
      .replace(/^orcid\.org\//, '');
    href = `https://orcid.org/${cleanId}`;
    displayText = `orcid.org/${cleanId}`;
    isLink = true;
  } else {
    let finalHrefPrefix = hrefPrefix;
    if (label === 'Website' && !value.startsWith('http') && !value.startsWith('//')) {
      finalHrefPrefix = 'https://';
    }
    href = finalHrefPrefix + value;
    isLink = href.startsWith('http') || href.startsWith('mailto:') || href.startsWith('tel:');
    if (label === 'Website' && isLink) {
      displayText = value.replace(/^https?:\/\//, '').replace(/^www\./, '');
    }
  }

  return { href, displayText, isLink };
}
