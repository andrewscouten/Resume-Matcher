/**
 * Cover Letter Settings
 *
 * Controls the visual appearance of the cover letter heading (letterhead).
 */

export type CoverLetterHeadingStyle = 'professional' | 'centered' | 'minimal';

export type CoverLetterHeadingField =
  | 'email'
  | 'phone'
  | 'location'
  | 'website'
  | 'linkedin'
  | 'github'
  | 'orcid';

export interface CoverLetterFontSizes {
  /** Candidate name in the letterhead (pt) */
  name: number;
  /** Contact info line in the letterhead (pt) */
  contact: number;
  /** Body paragraph text (pt) */
  body: number;
}

export interface CoverLetterSettings {
  /** Visual layout of the letterhead */
  headingStyle: CoverLetterHeadingStyle;
  /** Which contact info fields to display in the heading */
  headingFields: CoverLetterHeadingField[];
  /** Whether to show the candidate's job title below their name */
  showTitle: boolean;
  /** Font sizes for name, contact line, and body text (pt) */
  fontSizes: CoverLetterFontSizes;
}

export const DEFAULT_COVER_LETTER_SETTINGS: CoverLetterSettings = {
  headingStyle: 'professional',
  headingFields: ['email', 'phone', 'location', 'website', 'linkedin', 'github', 'orcid'],
  showTitle: true,
  fontSizes: {
    name: 22,
    contact: 10,
    body: 11,
  },
};

export const ALL_HEADING_FIELDS: CoverLetterHeadingField[] = [
  'email',
  'phone',
  'location',
  'website',
  'linkedin',
  'github',
  'orcid',
];

/** Contact-detail fields rendered on the first letterhead line. */
export const CONTACT_DETAIL_FIELDS: CoverLetterHeadingField[] = ['email', 'phone', 'location'];

/** Profile/identity link fields rendered on the second letterhead line. */
export const PROFILE_LINK_FIELDS: CoverLetterHeadingField[] = [
  'website',
  'linkedin',
  'github',
  'orcid',
];

/** Maps a heading field to the canonical contact label used for formatting. */
export const FIELD_TO_CONTACT_LABEL: Record<
  CoverLetterHeadingField,
  'Email' | 'Phone' | 'Location' | 'Website' | 'LinkedIn' | 'GitHub' | 'ORCID'
> = {
  email: 'Email',
  phone: 'Phone',
  location: 'Location',
  website: 'Website',
  linkedin: 'LinkedIn',
  github: 'GitHub',
  orcid: 'ORCID',
};

/** Href prefix for plain (non-URL) contact fields. */
export const FIELD_HREF_PREFIX: Partial<Record<CoverLetterHeadingField, string>> = {
  email: 'mailto:',
  phone: 'tel:',
};
