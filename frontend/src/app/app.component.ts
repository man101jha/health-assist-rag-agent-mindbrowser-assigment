import { Component, inject, ViewChild, ElementRef, AfterViewChecked } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChatService } from './services/chat.service';
import { MarkdownPipe } from './pipes/markdown.pipe';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule, MarkdownPipe],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent implements AfterViewChecked {
  @ViewChild('scrollContainer') private scrollContainer!: ElementRef;
  
  chatService = inject(ChatService);
  userInput = '';

  suggestions = [
    "How do I book an appointment?",
    "What are the signs of wound infection?",
    "Do you accept Medicaid?",
    "How do I manage pain after surgery?"
  ];

  ngAfterViewChecked() {
    this.scrollToBottom();
  }

  selectSuggestion(q: string) {
    this.userInput = q;
  }

  scrollToBottom(): void {
    try {
      this.scrollContainer.nativeElement.scrollTop = this.scrollContainer.nativeElement.scrollHeight;
    } catch(err) { }
  }

  onSend() {
    if (!this.userInput.trim()) return;
    this.chatService.sendMessage(this.userInput);
    this.userInput = '';
  }

  onSync() {
    if (confirm("Start Knowledge Synchronization? This will re-index all medical documents.")) {
      this.chatService.syncKnowledge().subscribe({
        next: () => alert("Sync Successful!"),
        error: () => alert("Sync Failed. Check backend logs.")
      });
    }
  }
}
