import { Pipe, PipeTransform } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

@Pipe({
  name: 'markdown',
  standalone: true
})
export class MarkdownPipe implements PipeTransform {
  constructor(private sanitizer: DomSanitizer) {}

  transform(value: string): SafeHtml {
    if (!value) return '';
    
    // Convert Markdown to simple HTML
    let html = value
      .replace(/### (.*)/g, '<h3>$1</h3>') // Headers
      .replace(/\*\*(.*)\*\*/g, '<strong>$1</strong>') // Bold
      .replace(/^- (.*)/gm, '<li>$1</li>') // Bullet points
      .replace(/\n/g, '<br>'); // New lines

    // Wrap list items in <ul> if they exist
    if (html.includes('<li>')) {
        // This is a simple fix for list wrapping
        html = html.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
    }

    return this.sanitizer.bypassSecurityTrustHtml(html);
  }
}
