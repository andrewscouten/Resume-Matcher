'use client';

import * as React from 'react';
import { Mail, Phone, MapPin, Globe, Linkedin, Github, ExternalLink } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useTranslations } from '@/lib/i18n';
import { formatContact, type ContactLabel } from '@/lib/utils/contact-info';
import {
  type CoverLetterSettings,
  type CoverLetterHeadingField,
  DEFAULT_COVER_LETTER_SETTINGS,
  type CoverLetterFontSizes,
  CONTACT_DETAIL_FIELDS,
  PROFILE_LINK_FIELDS,
  FIELD_TO_CONTACT_LABEL,
  FIELD_HREF_PREFIX,
} from '@/lib/types/cover-letter-settings';

export interface CoverLetterPersonalInfo {
  name?: string;
  title?: string;
  email?: string;
  phone?: string;
  location?: string;
  website?: string;
  linkedin?: string;
  github?: string;
  orcid?: string;
}

const CONTACT_ICONS: Record<ContactLabel, React.ReactNode> = {
  Email: <Mail size={12} />,
  Phone: <Phone size={12} />,
  Location: <MapPin size={12} />,
  Website: <Globe size={12} />,
  LinkedIn: <Linkedin size={12} />,
  GitHub: <Github size={12} />,
  ORCID: <ExternalLink size={12} />,
};

export interface CoverLetterPreviewProps {
  /** Cover letter content */
  content: string;
  /** Personal info for header */
  personalInfo: CoverLetterPersonalInfo;
  /** Page size for styling */
  pageSize?: 'A4' | 'LETTER';
  /** Heading/display settings */
  settings?: CoverLetterSettings;
  /** Additional class names */
  className?: string;
}

function ContactItem({
  field,
  personalInfo,
}: {
  field: CoverLetterHeadingField;
  personalInfo: CoverLetterPersonalInfo;
}) {
  const value = personalInfo[field];
  if (!value) return null;

  const label = FIELD_TO_CONTACT_LABEL[field];
  const { href, displayText, isLink } = formatContact(label, value, FIELD_HREF_PREFIX[field] ?? '');

  return (
    <span className="inline-flex items-center gap-1">
      {CONTACT_ICONS[label]}
      {isLink ? (
        <a
          href={href}
          target="_blank"
          rel="noopener noreferrer"
          className="text-hyper-blue hover:underline"
        >
          {displayText}
        </a>
      ) : (
        <span>{displayText}</span>
      )}
    </span>
  );
}

function ContactRow({
  personalInfo,
  fields,
  enabled,
  centered,
  fontSizes,
  className,
}: {
  personalInfo: CoverLetterPersonalInfo;
  fields: CoverLetterHeadingField[];
  enabled: CoverLetterHeadingField[];
  centered: boolean;
  fontSizes: CoverLetterFontSizes;
  className?: string;
}) {
  const visible = fields.filter((f) => enabled.includes(f) && !!personalInfo[f]);
  if (visible.length === 0) return null;

  return (
    <div
      className={cn(
        'flex flex-wrap gap-x-3 gap-y-1 font-mono leading-[1.6] text-ink',
        centered ? 'justify-center' : 'justify-start',
        className
      )}
      style={{ fontSize: `${fontSizes.contact}pt` }}
    >
      {visible.map((f) => (
        <ContactItem key={f} field={f} personalInfo={personalInfo} />
      ))}
    </div>
  );
}

function ContactLines({
  personalInfo,
  fields,
  style,
  fontSizes,
}: {
  personalInfo: CoverLetterPersonalInfo;
  fields: CoverLetterHeadingField[];
  style: CoverLetterSettings['headingStyle'];
  fontSizes: CoverLetterFontSizes;
}) {
  const centered = style === 'centered';

  return (
    <>
      <ContactRow
        personalInfo={personalInfo}
        fields={CONTACT_DETAIL_FIELDS}
        enabled={fields}
        centered={centered}
        fontSizes={fontSizes}
      />
      <ContactRow
        personalInfo={personalInfo}
        fields={PROFILE_LINK_FIELDS}
        enabled={fields}
        centered={centered}
        fontSizes={fontSizes}
        className="mt-1"
      />
    </>
  );
}

export function CoverLetterPreview({
  content,
  personalInfo,
  pageSize = 'A4',
  settings,
  className,
}: CoverLetterPreviewProps) {
  const { t, locale } = useTranslations();
  const s = settings ?? DEFAULT_COVER_LETTER_SETTINGS;
  const fs = s.fontSizes ?? DEFAULT_COVER_LETTER_SETTINGS.fontSizes;

  const today = new Intl.DateTimeFormat(locale, {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }).format(new Date());

  const paragraphs = content
    .split(/\n\n+/)
    .map((p) => p.trim())
    .filter((p) => p.length > 0);

  const centered = s.headingStyle === 'centered';
  const minimal = s.headingStyle === 'minimal';

  return (
    <div
      className={cn(
        'bg-white border-2 border-black',
        'shadow-sw-default',
        'overflow-hidden',
        className
      )}
    >
      <div
        className={cn('p-8 md:p-12', pageSize === 'A4' ? 'min-h-[297mm]' : 'min-h-[11in]')}
        style={{ maxWidth: pageSize === 'A4' ? '210mm' : '8.5in' }}
      >
        {/* Letterhead */}
        {minimal ? (
          /* Minimal (original) style */
          <header className="mb-8 border-b-2 border-black pb-4">
            <h1
              className="font-serif font-bold tracking-tight"
              style={{ fontSize: `${fs.name}pt` }}
            >
              {personalInfo.name || t('coverLetter.preview.defaultName')}
            </h1>
            <div className="mt-2">
              <ContactLines
                personalInfo={personalInfo}
                fields={s.headingFields}
                style={s.headingStyle}
                fontSizes={fs}
              />
            </div>
          </header>
        ) : (
          /* Professional / Centered styles */
          <header className={cn('mb-8 pb-4 border-b-2 border-black', centered && 'text-center')}>
            <h1
              className={cn(
                'font-serif font-bold tracking-[-0.01em] leading-none',
                centered && 'text-center'
              )}
              style={{ fontSize: `${fs.name}pt` }}
            >
              {personalInfo.name || t('coverLetter.preview.defaultName')}
            </h1>
            {s.showTitle && personalInfo.title && (
              <p className={cn('font-sans text-sm mt-1 text-ink-soft', centered && 'text-center')}>
                {personalInfo.title}
              </p>
            )}
            <div className="mt-3">
              <ContactLines
                personalInfo={personalInfo}
                fields={s.headingFields}
                style={s.headingStyle}
                fontSizes={fs}
              />
            </div>
          </header>
        )}

        {/* Date */}
        <div className="mb-8">
          <p className={cn('font-mono text-xs text-ink-soft', centered && 'text-center')}>
            {today}
          </p>
        </div>

        {/* Body */}
        <div className="space-y-4">
          {paragraphs.length > 0 ? (
            paragraphs.map((para, idx) => (
              <p
                key={idx}
                className="font-serif leading-relaxed text-ink"
                style={{ fontSize: `${fs.body}pt` }}
              >
                {para}
              </p>
            ))
          ) : (
            <div className="text-center py-12 text-steel-grey">
              <p className="font-mono text-sm">{t('coverLetter.preview.emptyTitle')}</p>
              <p className="font-mono text-xs mt-2">{t('coverLetter.preview.emptyDescription')}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
