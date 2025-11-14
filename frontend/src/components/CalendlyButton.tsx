/**
 * Calendly booking button component
 * Displays when demo booking tool is triggered
 */

interface CalendlyButtonProps {
  url: string;
}

export default function CalendlyButton({ url }: CalendlyButtonProps) {
  return (
    <div className="bg-green-50 border-2 border-green-500 rounded-lg p-4 mb-4">
      <div className="flex items-center gap-3">
        <div className="text-green-600 text-2xl">📅</div>
        <div className="flex-1">
          <h3 className="font-semibold text-green-900">Ready to schedule your demo!</h3>
          <p className="text-sm text-green-700">Click below to choose a time that works for you</p>
        </div>
      </div>
      <a
        href={url}
        target="_blank"
        rel="noopener noreferrer"
        className="mt-3 block w-full text-center bg-green-600 text-white py-2 px-4 rounded-lg hover:bg-green-700 transition-colors font-medium"
      >
        Schedule Demo
      </a>
    </div>
  );
}

